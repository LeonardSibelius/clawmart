"""
ClawMart — Seed Data
Pre-populate the registry with popular MCP servers.
"""

from database import get_db, add_server, get_server_count

SEED_SERVERS = [
    # ── Developer Tools ──
    {
        'name': 'filesystem',
        'description': 'Secure file operations with configurable access controls. Read, write, move, search, and manage files and directories on the local system.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem',
        'install_command': 'npx -y @modelcontextprotocol/server-filesystem /path/to/allowed',
        'transport_type': 'stdio',
        'categories': 'Developer Tools,Productivity',
        'capabilities': '{"tools": ["read_file", "write_file", "list_directory", "create_directory", "move_file", "search_files", "get_file_info"]}',
        'tags': 'file-system,local,read-write,directory'
    },
    {
        'name': 'github',
        'description': 'GitHub API integration for repository management, file operations, issues, pull requests, branches, and search across GitHub.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/github',
        'install_command': 'npx -y @modelcontextprotocol/server-github',
        'transport_type': 'stdio',
        'categories': 'Developer Tools',
        'capabilities': '{"tools": ["create_repository", "get_file_contents", "push_files", "create_issue", "create_pull_request", "search_repositories", "list_commits", "create_branch"]}',
        'tags': 'github,git,repository,code,version-control'
    },
    {
        'name': 'git',
        'description': 'Tools to read, search, and manipulate Git repositories. Access commit history, diffs, branches, and file contents from any local repo.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/git',
        'install_command': 'npx -y @modelcontextprotocol/server-git',
        'transport_type': 'stdio',
        'categories': 'Developer Tools',
        'capabilities': '{"tools": ["git_status", "git_log", "git_diff", "git_show", "git_branch_list", "git_checkout"]}',
        'tags': 'git,version-control,local,repository'
    },
    {
        'name': 'gitlab',
        'description': 'GitLab API integration for managing projects, merge requests, issues, pipelines, and repository operations.',
        'version': '2025.1',
        'author': 'Community',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/gitlab',
        'install_command': 'npx -y @modelcontextprotocol/server-gitlab',
        'transport_type': 'stdio',
        'categories': 'Developer Tools',
        'capabilities': '{"tools": ["create_project", "get_file", "create_merge_request", "list_pipelines", "create_issue"]}',
        'tags': 'gitlab,git,repository,ci-cd,devops'
    },
    # ── Data & Analytics ──
    {
        'name': 'postgres',
        'description': 'PostgreSQL database integration with schema inspection, read-only queries, and data analysis capabilities.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/postgres',
        'install_command': 'npx -y @modelcontextprotocol/server-postgres postgresql://localhost/mydb',
        'transport_type': 'stdio',
        'categories': 'Data & Analytics',
        'capabilities': '{"tools": ["query"], "resources": ["schema"]}',
        'tags': 'postgres,database,sql,query,analytics'
    },
    {
        'name': 'sqlite',
        'description': 'SQLite database operations including querying, schema exploration, data analysis, and business intelligence.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite',
        'install_command': 'npx -y @modelcontextprotocol/server-sqlite /path/to/database.db',
        'transport_type': 'stdio',
        'categories': 'Data & Analytics',
        'capabilities': '{"tools": ["read_query", "write_query", "create_table", "list_tables", "describe_table", "append_insight"]}',
        'tags': 'sqlite,database,sql,query,local'
    },
    {
        'name': 'bigquery',
        'description': 'Google BigQuery integration for running SQL queries, exploring datasets, and analyzing large-scale data.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/LucasHild/mcp-server-bigquery',
        'install_command': 'pip install mcp-server-bigquery',
        'transport_type': 'stdio',
        'categories': 'Data & Analytics',
        'capabilities': '{"tools": ["query", "list_datasets", "list_tables", "get_table_schema"]}',
        'tags': 'bigquery,google,database,sql,analytics,cloud'
    },
    # ── Web & Search ──
    {
        'name': 'brave-search',
        'description': 'Web and local search using Brave Search API. Provides both web results and local business/place information.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search',
        'install_command': 'npx -y @modelcontextprotocol/server-brave-search',
        'transport_type': 'stdio',
        'categories': 'Web & Search',
        'capabilities': '{"tools": ["brave_web_search", "brave_local_search"]}',
        'tags': 'search,web,brave,local-search'
    },
    {
        'name': 'fetch',
        'description': 'Web content fetching and conversion. Retrieves URLs and converts HTML to markdown for LLM-friendly consumption.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/fetch',
        'install_command': 'npx -y @modelcontextprotocol/server-fetch',
        'transport_type': 'stdio',
        'categories': 'Web & Search',
        'capabilities': '{"tools": ["fetch"]}',
        'tags': 'web,fetch,scrape,html,markdown'
    },
    {
        'name': 'puppeteer',
        'description': 'Browser automation using Puppeteer. Navigate pages, take screenshots, click elements, fill forms, and execute JavaScript.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer',
        'install_command': 'npx -y @modelcontextprotocol/server-puppeteer',
        'transport_type': 'stdio',
        'categories': 'Web & Search,Developer Tools',
        'capabilities': '{"tools": ["puppeteer_navigate", "puppeteer_screenshot", "puppeteer_click", "puppeteer_fill", "puppeteer_evaluate"]}',
        'tags': 'browser,automation,puppeteer,screenshot,scraping'
    },
    {
        'name': 'playwright',
        'description': 'Browser automation with Playwright. Full browser control: navigation, screenshots, form filling, and JavaScript execution.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/executeautomation/mcp-playwright',
        'install_command': 'npx @playwright/mcp@latest',
        'transport_type': 'stdio',
        'categories': 'Web & Search,Developer Tools',
        'capabilities': '{"tools": ["navigate", "screenshot", "click", "fill", "select", "evaluate"]}',
        'tags': 'browser,automation,playwright,testing,scraping'
    },
    # ── Communication ──
    {
        'name': 'slack',
        'description': 'Slack workspace integration. Read channels, post messages, manage threads, add reactions, and search conversation history.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/slack',
        'install_command': 'npx -y @modelcontextprotocol/server-slack',
        'transport_type': 'stdio',
        'categories': 'Communication,Productivity',
        'capabilities': '{"tools": ["list_channels", "post_message", "reply_to_thread", "add_reaction", "get_channel_history", "search_messages"]}',
        'tags': 'slack,messaging,team,communication,channels'
    },
    {
        'name': 'gmail',
        'description': 'Gmail integration for reading, searching, sending, and managing email. Full inbox management with label support.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholishen/mcp-gmail',
        'install_command': 'pip install mcp-gmail',
        'transport_type': 'stdio',
        'categories': 'Communication,Productivity',
        'capabilities': '{"tools": ["read_email", "send_email", "search_emails", "list_labels", "modify_labels"]}',
        'tags': 'gmail,email,google,communication,inbox'
    },
    {
        'name': 'discord',
        'description': 'Discord bot integration for reading messages, posting to channels, managing servers, and interacting with users.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/v-3/mcp-discord',
        'install_command': 'npx mcp-discord',
        'transport_type': 'stdio',
        'categories': 'Communication',
        'capabilities': '{"tools": ["send_message", "read_messages", "list_channels", "list_servers"]}',
        'tags': 'discord,messaging,community,chat'
    },
    # ── Productivity ──
    {
        'name': 'google-drive',
        'description': 'Google Drive integration for searching, reading, and managing files. Access docs, sheets, and other Drive content.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/google-drive',
        'install_command': 'npx -y @modelcontextprotocol/server-google-drive',
        'transport_type': 'stdio',
        'categories': 'Productivity,Data & Analytics',
        'capabilities': '{"tools": ["search_files", "read_file", "list_files"]}',
        'tags': 'google-drive,files,documents,cloud-storage'
    },
    {
        'name': 'google-maps',
        'description': 'Google Maps Platform integration for geocoding, directions, place search, elevation, and distance calculations.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps',
        'install_command': 'npx -y @modelcontextprotocol/server-google-maps',
        'transport_type': 'stdio',
        'categories': 'Productivity,Web & Search',
        'capabilities': '{"tools": ["geocode", "reverse_geocode", "search_places", "get_directions", "get_distance_matrix", "get_elevation"]}',
        'tags': 'google-maps,location,geocoding,directions,places'
    },
    {
        'name': 'notion',
        'description': 'Notion workspace integration. Search pages, read and create content, manage databases, and organize knowledge bases.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/suekou/mcp-notion-server',
        'install_command': 'npx mcp-notion-server',
        'transport_type': 'stdio',
        'categories': 'Productivity',
        'capabilities': '{"tools": ["search", "get_page", "create_page", "update_page", "query_database", "create_database"]}',
        'tags': 'notion,notes,wiki,database,knowledge-base'
    },
    {
        'name': 'linear',
        'description': 'Linear project management integration. Create and manage issues, projects, and team workflows.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/jerhadf/linear-mcp-server',
        'install_command': 'npx linear-mcp-server',
        'transport_type': 'stdio',
        'categories': 'Productivity,Developer Tools',
        'capabilities': '{"tools": ["create_issue", "update_issue", "search_issues", "list_projects", "list_teams"]}',
        'tags': 'linear,project-management,issues,agile,tasks'
    },
    {
        'name': 'todoist',
        'description': 'Todoist task management. Create, update, complete, and organize tasks and projects.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/abhiz123/todoist-mcp-server',
        'install_command': 'npx todoist-mcp-server',
        'transport_type': 'stdio',
        'categories': 'Productivity',
        'capabilities': '{"tools": ["create_task", "get_tasks", "update_task", "complete_task", "list_projects"]}',
        'tags': 'todoist,tasks,todo,productivity,planning'
    },
    # ── AI / ML ──
    {
        'name': 'memory',
        'description': 'Knowledge graph-based persistent memory. Store entities, relationships, and observations across conversations.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/memory',
        'install_command': 'npx -y @modelcontextprotocol/server-memory',
        'transport_type': 'stdio',
        'categories': 'AI & ML',
        'capabilities': '{"tools": ["create_entities", "create_relations", "add_observations", "search_nodes", "open_nodes", "delete_entities"]}',
        'tags': 'memory,knowledge-graph,persistent,entities,relations'
    },
    {
        'name': 'sequential-thinking',
        'description': 'Dynamic problem-solving through sequential thought chains. Supports branching, revision, and hypothesis exploration.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking',
        'install_command': 'npx -y @modelcontextprotocol/server-sequential-thinking',
        'transport_type': 'stdio',
        'categories': 'AI & ML',
        'capabilities': '{"tools": ["sequentialthinking"]}',
        'tags': 'reasoning,thinking,chain-of-thought,problem-solving'
    },
    {
        'name': 'exa',
        'description': 'Exa AI-powered search. Semantic search, keyword search, and content retrieval with AI-optimized results.',
        'version': '0.1.0',
        'author': 'Exa',
        'repo_url': 'https://github.com/exa-labs/exa-mcp-server',
        'install_command': 'npx exa-mcp-server',
        'transport_type': 'stdio',
        'categories': 'AI & ML,Web & Search',
        'capabilities': '{"tools": ["search", "find_similar", "get_contents"]}',
        'tags': 'search,ai,semantic,exa,web-search'
    },
    {
        'name': 'rag-docs',
        'description': 'RAG (Retrieval Augmented Generation) over local documents. Index and query PDF, markdown, and text files.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-rag-docs',
        'install_command': 'npx mcp-rag-docs',
        'transport_type': 'stdio',
        'categories': 'AI & ML,Data & Analytics',
        'capabilities': '{"tools": ["index_document", "query_documents", "list_documents"]}',
        'tags': 'rag,documents,embeddings,search,local'
    },
    # ── Infrastructure ──
    {
        'name': 'docker',
        'description': 'Docker container management. List, start, stop, and inspect containers, images, volumes, and networks.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/QuantGeekDev/docker-mcp',
        'install_command': 'npx docker-mcp',
        'transport_type': 'stdio',
        'categories': 'Infrastructure,Developer Tools',
        'capabilities': '{"tools": ["list_containers", "start_container", "stop_container", "run_container", "list_images", "pull_image"]}',
        'tags': 'docker,containers,devops,infrastructure'
    },
    {
        'name': 'kubernetes',
        'description': 'Kubernetes cluster management. List pods, deployments, services. Apply and delete resources. View logs.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/strowk/mcp-k8s',
        'install_command': 'npx mcp-k8s',
        'transport_type': 'stdio',
        'categories': 'Infrastructure',
        'capabilities': '{"tools": ["list_pods", "list_deployments", "list_services", "apply_resource", "delete_resource", "get_logs"]}',
        'tags': 'kubernetes,k8s,containers,orchestration,devops'
    },
    {
        'name': 'aws',
        'description': 'AWS cloud services integration. Manage S3 buckets, EC2 instances, Lambda functions, and other AWS resources.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/rishikavikondala/mcp-server-aws',
        'install_command': 'pip install mcp-server-aws',
        'transport_type': 'stdio',
        'categories': 'Infrastructure',
        'capabilities': '{"tools": ["s3_list_buckets", "s3_get_object", "s3_put_object", "ec2_describe_instances", "lambda_invoke"]}',
        'tags': 'aws,cloud,s3,ec2,lambda,infrastructure'
    },
    {
        'name': 'cloudflare',
        'description': 'Cloudflare management via API. Configure DNS, manage Workers, adjust security settings, and view analytics.',
        'version': '0.1.0',
        'author': 'Cloudflare',
        'repo_url': 'https://github.com/cloudflare/mcp-server-cloudflare',
        'install_command': 'npx @cloudflare/mcp-server-cloudflare',
        'transport_type': 'stdio',
        'categories': 'Infrastructure,Web & Search',
        'capabilities': '{"tools": ["list_zones", "create_dns_record", "list_workers", "deploy_worker", "get_analytics"]}',
        'tags': 'cloudflare,dns,workers,cdn,security'
    },
    {
        'name': 'vercel',
        'description': 'Vercel deployment platform integration. Manage projects, deployments, domains, and environment variables.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-vercel',
        'install_command': 'npx mcp-vercel',
        'transport_type': 'stdio',
        'categories': 'Infrastructure,Developer Tools',
        'capabilities': '{"tools": ["list_projects", "create_deployment", "list_deployments", "manage_domains", "set_env_vars"]}',
        'tags': 'vercel,deployment,hosting,serverless,frontend'
    },
    # ── Data & Files ──
    {
        'name': 'everything',
        'description': 'Reference MCP server that exercises all protocol features. Useful for testing MCP clients and understanding the protocol.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/everything',
        'install_command': 'npx -y @modelcontextprotocol/server-everything',
        'transport_type': 'stdio',
        'categories': 'Developer Tools',
        'capabilities': '{"tools": ["echo", "add", "longRunningOperation", "sampleLLM", "getTinyImage"], "resources": ["file", "text"], "prompts": ["simple_prompt", "complex_prompt"]}',
        'tags': 'reference,testing,protocol,example'
    },
    {
        'name': 'sentry',
        'description': 'Sentry error tracking integration. View issues, get stack traces, analyze error trends, and manage releases.',
        'version': '0.1.0',
        'author': 'Sentry',
        'repo_url': 'https://github.com/getsentry/sentry-mcp',
        'install_command': 'npx @sentry/mcp-server',
        'transport_type': 'stdio',
        'categories': 'Developer Tools,Infrastructure',
        'capabilities': '{"tools": ["list_issues", "get_issue_details", "search_issues", "get_event"]}',
        'tags': 'sentry,errors,monitoring,debugging,observability'
    },
    {
        'name': 'stripe',
        'description': 'Stripe payment integration. Manage customers, products, prices, subscriptions, and payment processing.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/stripe/agent-toolkit',
        'install_command': 'npx @stripe/mcp',
        'transport_type': 'stdio',
        'categories': 'Infrastructure,Productivity',
        'capabilities': '{"tools": ["create_customer", "create_product", "create_price", "create_payment_link", "list_customers"]}',
        'tags': 'stripe,payments,billing,subscriptions,commerce'
    },
    {
        'name': 'twilio',
        'description': 'Twilio communications. Send SMS, make calls, manage phone numbers, and handle messaging workflows.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/twilio/mcp-server-twilio',
        'install_command': 'npx @twilio/mcp-server',
        'transport_type': 'stdio',
        'categories': 'Communication,Infrastructure',
        'capabilities': '{"tools": ["send_sms", "make_call", "list_messages", "list_phone_numbers"]}',
        'tags': 'twilio,sms,voice,phone,communication'
    },
    {
        'name': 'figma',
        'description': 'Figma design tool integration. Read file contents, get component info, export assets, and inspect design tokens.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-figma',
        'install_command': 'npx mcp-figma',
        'transport_type': 'stdio',
        'categories': 'Developer Tools,Productivity',
        'capabilities': '{"tools": ["get_file", "get_components", "get_styles", "export_assets"]}',
        'tags': 'figma,design,ui,components,assets'
    },
    {
        'name': 'airtable',
        'description': 'Airtable database integration. Read, create, update records in bases and tables. Query with filters and sorts.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-airtable',
        'install_command': 'npx mcp-airtable',
        'transport_type': 'stdio',
        'categories': 'Data & Analytics,Productivity',
        'capabilities': '{"tools": ["list_bases", "list_records", "create_record", "update_record", "search_records"]}',
        'tags': 'airtable,database,spreadsheet,no-code,records'
    },
    {
        'name': 'supabase',
        'description': 'Supabase backend-as-a-service integration. Database queries, auth management, storage, and edge functions.',
        'version': '0.1.0',
        'author': 'Supabase',
        'repo_url': 'https://github.com/supabase/mcp-server-supabase',
        'install_command': 'npx mcp-server-supabase',
        'transport_type': 'stdio',
        'categories': 'Infrastructure,Data & Analytics',
        'capabilities': '{"tools": ["query", "insert", "update", "delete", "list_tables", "manage_auth"]}',
        'tags': 'supabase,database,postgres,auth,backend,baas'
    },
    {
        'name': 'redis',
        'description': 'Redis key-value store integration. Get, set, delete keys. Work with lists, sets, hashes, and pub/sub.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-redis',
        'install_command': 'npx mcp-redis',
        'transport_type': 'stdio',
        'categories': 'Data & Analytics,Infrastructure',
        'capabilities': '{"tools": ["get", "set", "delete", "list_keys", "hget", "hset", "lpush", "lrange"]}',
        'tags': 'redis,cache,key-value,database,pubsub'
    },
    {
        'name': 'mysql',
        'description': 'MySQL database integration. Execute queries, explore schemas, manage tables, and analyze data.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-mysql',
        'install_command': 'npx mcp-mysql',
        'transport_type': 'stdio',
        'categories': 'Data & Analytics',
        'capabilities': '{"tools": ["query", "list_databases", "list_tables", "describe_table"]}',
        'tags': 'mysql,database,sql,query,relational'
    },
    {
        'name': 'mongodb',
        'description': 'MongoDB integration. Query collections, insert/update documents, aggregate data, and manage indexes.',
        'version': '0.1.0',
        'author': 'MongoDB',
        'repo_url': 'https://github.com/mongodb-js/mongodb-mcp-server',
        'install_command': 'npx mongodb-mcp-server',
        'transport_type': 'stdio',
        'categories': 'Data & Analytics',
        'capabilities': '{"tools": ["find", "insert_one", "update_one", "aggregate", "list_collections", "create_index"]}',
        'tags': 'mongodb,database,nosql,documents,aggregation'
    },
    {
        'name': 'time',
        'description': 'Time and timezone utilities. Get current time in any timezone, convert between zones, and calculate durations.',
        'version': '2025.1',
        'author': 'Anthropic',
        'repo_url': 'https://github.com/modelcontextprotocol/servers/tree/main/src/time',
        'install_command': 'npx -y @modelcontextprotocol/server-time',
        'transport_type': 'stdio',
        'categories': 'Productivity',
        'capabilities': '{"tools": ["get_current_time", "convert_timezone"]}',
        'tags': 'time,timezone,clock,date,utility'
    },
    {
        'name': 'weather',
        'description': 'National Weather Service API integration. Get current conditions, forecasts, and weather alerts for US locations.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/modelcontextprotocol/quickstart-resources',
        'install_command': 'pip install mcp-weather',
        'transport_type': 'stdio',
        'categories': 'Web & Search',
        'capabilities': '{"tools": ["get_forecast", "get_alerts"]}',
        'tags': 'weather,forecast,alerts,nws,location'
    },
    {
        'name': 'youtube-transcript',
        'description': 'Extract transcripts and captions from YouTube videos. Supports multiple languages and auto-generated captions.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-youtube-transcript',
        'install_command': 'npx mcp-youtube-transcript',
        'transport_type': 'stdio',
        'categories': 'Data & Analytics,AI & ML',
        'capabilities': '{"tools": ["get_transcript"]}',
        'tags': 'youtube,transcript,captions,video,subtitles'
    },
    {
        'name': 'obsidian',
        'description': 'Obsidian vault integration. Read, create, search, and manage markdown notes in your knowledge base.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-obsidian',
        'install_command': 'npx mcp-obsidian',
        'transport_type': 'stdio',
        'categories': 'Productivity',
        'capabilities': '{"tools": ["read_note", "create_note", "search_notes", "list_notes", "update_note"]}',
        'tags': 'obsidian,notes,markdown,knowledge-base,pkm'
    },
    {
        'name': 'jira',
        'description': 'Jira project management integration. Create issues, search, update status, manage sprints and boards.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-jira',
        'install_command': 'npx mcp-jira',
        'transport_type': 'stdio',
        'categories': 'Productivity,Developer Tools',
        'capabilities': '{"tools": ["create_issue", "search_issues", "update_issue", "list_projects", "get_board"]}',
        'tags': 'jira,project-management,issues,agile,sprints'
    },
    {
        'name': 'confluence',
        'description': 'Atlassian Confluence integration. Search, read, create, and update pages in your team wiki.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-confluence',
        'install_command': 'npx mcp-confluence',
        'transport_type': 'stdio',
        'categories': 'Productivity',
        'capabilities': '{"tools": ["search_pages", "get_page", "create_page", "update_page", "list_spaces"]}',
        'tags': 'confluence,wiki,documentation,knowledge-base,atlassian'
    },
    {
        'name': 'shopify',
        'description': 'Shopify store management. Products, orders, customers, inventory, and storefront operations.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-shopify',
        'install_command': 'npx mcp-shopify',
        'transport_type': 'stdio',
        'categories': 'Productivity,Infrastructure',
        'capabilities': '{"tools": ["list_products", "create_product", "list_orders", "get_customer", "update_inventory"]}',
        'tags': 'shopify,ecommerce,products,orders,store'
    },
    {
        'name': 'hubspot',
        'description': 'HubSpot CRM integration. Manage contacts, deals, companies, and marketing campaigns.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-hubspot',
        'install_command': 'npx mcp-hubspot',
        'transport_type': 'stdio',
        'categories': 'Productivity,Communication',
        'capabilities': '{"tools": ["list_contacts", "create_contact", "list_deals", "create_deal", "search_contacts"]}',
        'tags': 'hubspot,crm,contacts,deals,marketing'
    },
    {
        'name': 'asana',
        'description': 'Asana work management. Create tasks, manage projects, track goals, and organize team workflows.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-asana',
        'install_command': 'npx mcp-asana',
        'transport_type': 'stdio',
        'categories': 'Productivity',
        'capabilities': '{"tools": ["create_task", "list_tasks", "update_task", "list_projects", "list_workspaces"]}',
        'tags': 'asana,project-management,tasks,teams,workflow'
    },
    {
        'name': 'trello',
        'description': 'Trello board management. Create cards, manage lists, update boards, and organize kanban workflows.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/nicholasgriffintn/mcp-trello',
        'install_command': 'npx mcp-trello',
        'transport_type': 'stdio',
        'categories': 'Productivity',
        'capabilities': '{"tools": ["create_card", "list_cards", "move_card", "list_boards", "list_lists"]}',
        'tags': 'trello,kanban,boards,cards,project-management'
    },
    {
        'name': 'pinecone',
        'description': 'Pinecone vector database integration. Upsert, query, and manage vector embeddings for similarity search.',
        'version': '0.1.0',
        'author': 'Pinecone',
        'repo_url': 'https://github.com/pinecone-io/pinecone-mcp',
        'install_command': 'npx @pinecone-database/mcp',
        'transport_type': 'stdio',
        'categories': 'AI & ML,Data & Analytics',
        'capabilities': '{"tools": ["upsert_vectors", "query_vectors", "list_indexes", "create_index", "describe_index"]}',
        'tags': 'pinecone,vector,embeddings,similarity,search'
    },
    {
        'name': 'weaviate',
        'description': 'Weaviate vector database. Store, search, and manage objects with vector and keyword search capabilities.',
        'version': '0.1.0',
        'author': 'Community',
        'repo_url': 'https://github.com/weaviate/mcp-server-weaviate',
        'install_command': 'npx mcp-server-weaviate',
        'transport_type': 'stdio',
        'categories': 'AI & ML,Data & Analytics',
        'capabilities': '{"tools": ["add_objects", "search", "list_collections", "create_collection"]}',
        'tags': 'weaviate,vector,database,search,embeddings'
    },
]


def seed_if_empty():
    """Seed the database if no servers exist."""
    if get_server_count() > 0:
        print(f"[Seed] Database already has {get_server_count()} servers, skipping seed.")
        return

    print(f"[Seed] Seeding {len(SEED_SERVERS)} MCP servers...")
    for server in SEED_SERVERS:
        try:
            add_server(server)
        except Exception as e:
            print(f"[Seed] Error adding {server['name']}: {e}")

    print(f"[Seed] Done. {get_server_count()} servers in registry.")


if __name__ == '__main__':
    from database import init_db
    init_db()
    seed_if_empty()
